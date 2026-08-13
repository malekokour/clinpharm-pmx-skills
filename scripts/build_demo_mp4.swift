#!/usr/bin/env swift
// Build the captioned ClinPharm PMx Skills workflow MP4 from committed synthetic frames.
// Author: ClinPharm PMx Skills contributors
// Date: 2026-07-30
// Dependencies: macOS AVFoundation and CoreGraphics

import AVFoundation
import CoreGraphics
import Foundation
import ImageIO

let width = 1280
let height = 720
let framesPerSecond: Int32 = 2
let frameDurations = [5, 5, 5, 5, 6, 6]

func fail(_ message: String) -> Never {
    FileHandle.standardError.write(Data("ERROR: \(message)\n".utf8))
    exit(1)
}

func loadImage(_ url: URL) -> CGImage {
    guard
        let source = CGImageSourceCreateWithURL(url as CFURL, nil),
        let image = CGImageSourceCreateImageAtIndex(source, 0, nil)
    else {
        fail("could not read \(url.path)")
    }
    guard image.width == width, image.height == height else {
        fail("expected \(width)x\(height), found \(image.width)x\(image.height): \(url.path)")
    }
    return image
}

func makePixelBuffer(_ image: CGImage, pool: CVPixelBufferPool) -> CVPixelBuffer {
    var optionalBuffer: CVPixelBuffer?
    guard CVPixelBufferPoolCreatePixelBuffer(nil, pool, &optionalBuffer) == kCVReturnSuccess,
          let buffer = optionalBuffer
    else {
        fail("could not allocate a video frame")
    }

    CVPixelBufferLockBaseAddress(buffer, [])
    defer { CVPixelBufferUnlockBaseAddress(buffer, []) }

    guard
        let baseAddress = CVPixelBufferGetBaseAddress(buffer),
        let context = CGContext(
            data: baseAddress,
            width: width,
            height: height,
            bitsPerComponent: 8,
            bytesPerRow: CVPixelBufferGetBytesPerRow(buffer),
            space: CGColorSpaceCreateDeviceRGB(),
            bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue
        )
    else {
        fail("could not create the frame drawing context")
    }

    context.draw(image, in: CGRect(x: 0, y: 0, width: width, height: height))
    return buffer
}

guard CommandLine.arguments.count == 3 else {
    fail("usage: build_demo_mp4.swift <frames-directory> <output.mp4>")
}

let framesDirectory = URL(fileURLWithPath: CommandLine.arguments[1], isDirectory: true)
let outputURL = URL(fileURLWithPath: CommandLine.arguments[2])
let frameURLs = (1...frameDurations.count).map {
    framesDirectory.appendingPathComponent(String(format: "workflow-%02d.png", $0))
}

for url in frameURLs where !FileManager.default.fileExists(atPath: url.path) {
    fail("missing frame: \(url.path)")
}

try? FileManager.default.removeItem(at: outputURL)

let writer: AVAssetWriter
do {
    writer = try AVAssetWriter(outputURL: outputURL, fileType: .mp4)
} catch {
    fail("could not create MP4 writer: \(error.localizedDescription)")
}

let videoSettings: [String: Any] = [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: width,
    AVVideoHeightKey: height,
    AVVideoCompressionPropertiesKey: [
        AVVideoAverageBitRateKey: 2_500_000,
        AVVideoExpectedSourceFrameRateKey: framesPerSecond,
        AVVideoMaxKeyFrameIntervalKey: framesPerSecond * 2,
        AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
    ],
]

let input = AVAssetWriterInput(mediaType: .video, outputSettings: videoSettings)
input.expectsMediaDataInRealTime = false
guard writer.canAdd(input) else {
    fail("AVFoundation rejected the video settings")
}
writer.add(input)

let pixelBufferAttributes: [String: Any] = [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32ARGB,
    kCVPixelBufferWidthKey as String: width,
    kCVPixelBufferHeightKey as String: height,
]
let adaptor = AVAssetWriterInputPixelBufferAdaptor(
    assetWriterInput: input,
    sourcePixelBufferAttributes: pixelBufferAttributes
)

guard writer.startWriting() else {
    fail(writer.error?.localizedDescription ?? "could not start MP4 writer")
}
writer.startSession(atSourceTime: .zero)

guard let pool = adaptor.pixelBufferPool else {
    fail("AVFoundation did not create a pixel-buffer pool")
}

var frameNumber: Int64 = 0
for (index, url) in frameURLs.enumerated() {
    let image = loadImage(url)
    let repeatCount = frameDurations[index] * Int(framesPerSecond)
    for _ in 0..<repeatCount {
        while !input.isReadyForMoreMediaData {
            Thread.sleep(forTimeInterval: 0.01)
        }
        let buffer = makePixelBuffer(image, pool: pool)
        let presentationTime = CMTime(value: frameNumber, timescale: framesPerSecond)
        guard adaptor.append(buffer, withPresentationTime: presentationTime) else {
            fail(writer.error?.localizedDescription ?? "could not append frame")
        }
        frameNumber += 1
    }
}

input.markAsFinished()
let finished = DispatchSemaphore(value: 0)
writer.finishWriting {
    finished.signal()
}
finished.wait()

guard writer.status == .completed else {
    fail(writer.error?.localizedDescription ?? "MP4 writer did not complete")
}

let duration = Double(frameNumber) / Double(framesPerSecond)
print("Built \(outputURL.path) (\(String(format: "%.1f", duration)) seconds)")

import Foundation
import MinuteMosaic

// mm-timeline: a tiny local CLI that loads a minutemosaic report JSON (produced
// by the Python side) and renders the evidence timeline as text or SVG.
//
// Usage:
//   mm-timeline <report.json> [--svg out.svg] [--share-safe]
//
// No network. No audio. It only reads local JSON and writes local files.

func fail(_ message: String) -> Never {
    FileHandle.standardError.write(Data((message + "\n").utf8))
    exit(2)
}

let args = Array(CommandLine.arguments.dropFirst())
guard let path = args.first, !path.hasPrefix("--") else {
    fail("usage: mm-timeline <report.json> [--svg out.svg] [--share-safe]")

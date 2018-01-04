import Foundation

/// A single timestamped, attributed line of transcript.
///
/// This mirrors the Python `Utterance`: `index` is the atomic unit of
/// provenance. The Swift side is a *local* model only — it performs no audio
/// processing and makes no transcription claims. It consumes transcripts that
/// were produced elsewhere.
public struct Utterance: Codable, Identifiable, Equatable {
    public let index: Int
    public let start: TimeInterval

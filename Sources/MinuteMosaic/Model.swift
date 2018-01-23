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
    public let end: TimeInterval
    public let speaker: String
    public let text: String

    public var id: Int { index }
    public var duration: TimeInterval { max(0, end - start) }

    public init(index: Int, start: TimeInterval, end: TimeInterval, speaker: String, text: String) {
        self.index = index
        self.start = start
        self.end = end
        self.speaker = speaker
        self.text = text
    }
}

/// Evidence attached to a derived claim: which rule fired, on what trigger, and
/// which utterance indices are the source spans.
public struct Provenance: Codable, Equatable {
    public let ruleID: String
    public let trigger: String
    public let utteranceIndices: [Int]
    public let note: String

    public init(ruleID: String, trigger: String, utteranceIndices: [Int], note: String = "") {
        self.ruleID = ruleID
        self.trigger = trigger
        self.utteranceIndices = utteranceIndices
        self.note = note
    }

    enum CodingKeys: String, CodingKey {
        case ruleID = "rule_id"

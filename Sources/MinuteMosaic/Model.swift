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
        case trigger
        case utteranceIndices = "utterance_indices"
        case note
    }
}

/// Kinds of derived events that can appear on the evidence timeline.
public enum EventKind: String, Codable {
    case topic
    case decision
    case action
}

/// A derived, evidence-backed event positioned on the meeting timeline.
public struct TimelineEvent: Codable, Identifiable, Equatable {
    public let id: Int
    public let kind: EventKind
    public let time: TimeInterval
    public let label: String
    public let detail: String
    public let confidence: Double
    public let provenance: Provenance?

    public init(
        id: Int,
        kind: EventKind,
        time: TimeInterval,
        label: String,
        detail: String,
        confidence: Double,
        provenance: Provenance?
    ) {
        self.id = id
        self.kind = kind
        self.time = time
        self.label = label
        self.detail = detail
        self.confidence = confidence
        self.provenance = provenance
    }
}

/// A whole meeting: the transcript plus derived events. This is the local
/// document type the app persists; there is no remote service involved.
public struct Meeting: Codable, Equatable {
    public let title: String
    public let source: String
    public var utterances: [Utterance]
    public var events: [TimelineEvent]

    public init(title: String, source: String, utterances: [Utterance], events: [TimelineEvent] = []) {

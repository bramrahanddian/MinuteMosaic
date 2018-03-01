import Foundation

/// Privacy and retention policy for locally stored meetings.
///
/// minutemosaic is local-first: nothing here uploads data anywhere. These
/// settings govern how long transcripts live on disk and whether raw text is
/// redacted when exporting the evidence timeline.
public struct PrivacySettings: Codable, Equatable {
    /// How long to keep meeting documents before they are eligible for pruning.
    public enum Retention: Codable, Equatable {
        case forever
        case days(Int)

        /// Cutoff date before which meetings are expired, relative to `now`.
        public func cutoff(from now: Date) -> Date? {
            switch self {
            case .forever:
                return nil
            case .days(let d):
                return Calendar.current.date(byAdding: .day, value: -d, to: now)
            }
        }
    }

    /// Retain everything by default; the user chooses to shorten this.
    public var retention: Retention
    /// If true, exports replace utterance text with a length-preserving mask so
    /// the timeline shape is shareable without leaking content.
    public var redactTranscriptOnExport: Bool
    /// If true, speaker names are replaced with stable pseudonyms on export.
    public var pseudonymizeSpeakers: Bool

    public init(

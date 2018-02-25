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

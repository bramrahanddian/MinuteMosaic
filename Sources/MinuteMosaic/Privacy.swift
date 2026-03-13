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
        retention: Retention = .forever,
        redactTranscriptOnExport: Bool = false,
        pseudonymizeSpeakers: Bool = false
    ) {
        self.retention = retention
        self.redactTranscriptOnExport = redactTranscriptOnExport
        self.pseudonymizeSpeakers = pseudonymizeSpeakers
    }

    /// A conservative, share-friendly preset.
    public static let shareSafe = PrivacySettings(
        retention: .days(30),
        redactTranscriptOnExport: true,
        pseudonymizeSpeakers: true
    )
}

public enum RetentionEngine {
    /// Return true if a meeting recorded at `recordedAt` should be pruned under
    /// `settings` as of `now`.
    public static func isExpired(recordedAt: Date, settings: PrivacySettings, now: Date = Date()) -> Bool {
        guard let cutoff = settings.retention.cutoff(from: now) else { return false }
        return recordedAt < cutoff
    }

    /// Apply export-time privacy transforms to a meeting, returning a copy.
    public static func applyExportPolicy(to meeting: Meeting, settings: PrivacySettings) -> Meeting {
        guard settings.redactTranscriptOnExport || settings.pseudonymizeSpeakers else {
            return meeting
        }

        var speakerMap: [String: String] = [:]
        var nextSpeaker = 0

        func pseudonym(for name: String) -> String {
            if let existing = speakerMap[name] { return existing }
            let alias = "Speaker \(Character(UnicodeScalar(65 + (nextSpeaker % 26))!))"
            nextSpeaker += 1
            speakerMap[name] = alias
            return alias
        }

        let transformed = meeting.utterances.map { u -> Utterance in
            let speaker = settings.pseudonymizeSpeakers ? pseudonym(for: u.speaker) : u.speaker
            let text = settings.redactTranscriptOnExport ? RetentionEngine.mask(u.text) : u.text
            return Utterance(index: u.index, start: u.start, end: u.end, speaker: speaker, text: text)
        }

        return Meeting(title: meeting.title, source: meeting.source, utterances: transformed, events: meeting.events)
    }

    /// Replace word characters with a bullet, preserving whitespace so the
    /// visible rhythm of the transcript survives while content does not.
    static func mask(_ text: String) -> String {
        String(text.map { $0.isWhitespace ? $0 : "•" })
    }
}

<!-- draft note 1416 -->

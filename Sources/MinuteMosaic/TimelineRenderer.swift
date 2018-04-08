import Foundation

/// Renders the evidence timeline to portable text formats. Everything is local;
/// no network calls are made. The renderer is intentionally UI-framework-free so
/// it builds on any platform (including headless CI) — a SwiftUI view can layer
/// on top of these primitives.
public enum TimelineRenderer {

    /// A laid-out facet for a single utterance, normalized to `0...1` on x.
    public struct Facet: Equatable {
        public let utteranceIndex: Int
        public let x: Double
        public let width: Double
        public let speaker: String
    }

    /// Compute stained-glass facets across the meeting span.
    public static func facets(for meeting: Meeting) -> [Facet] {
        guard let first = meeting.utterances.first else { return [] }
        let span = max(0.000001, meeting.span)
        let t0 = first.start
        return meeting.utterances.map { u in
            Facet(
                utteranceIndex: u.index,
                x: (u.start - t0) / span,
                width: max(0.004, u.duration / span),
                speaker: u.speaker
            )
        }
    }

    private static func fmt(_ t: TimeInterval) -> String {
        let s = Int(t.rounded())
        return String(format: "%02d:%02d", s / 60, s % 60)
    }

    /// A compact, human-readable evidence timeline as plain text.
    public static func renderText(_ meeting: Meeting) -> String {
        var lines: [String] = []
        lines.append("# \(meeting.title)")
        lines.append("source: \(meeting.source) · span \(fmt(meeting.span)) · local-first, offline")

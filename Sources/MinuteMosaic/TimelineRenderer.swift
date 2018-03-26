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

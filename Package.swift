// swift-tools-version:5.7
import PackageDescription

let package = Package(
    name: "MinuteMosaic",
    platforms: [
        .macOS(.v12),
        .iOS(.v15),
    ],
    products: [
        .library(name: "MinuteMosaic", targets: ["MinuteMosaic"]),
        .executable(name: "mm-timeline", targets: ["mm-timeline"]),
    ],
    targets: [
        .target(
            name: "MinuteMosaic",
            path: "Sources/MinuteMosaic"
        ),
        .executableTarget(

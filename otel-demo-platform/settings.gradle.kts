pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}

rootProject.name = "otel-demo-platform"
include("api", "worker", "contracts")

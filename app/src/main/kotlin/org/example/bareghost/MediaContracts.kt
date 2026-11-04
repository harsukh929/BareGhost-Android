package org.example.bareghost

data class MediaCandidate(val pageUrl: String, val mediaUrl: String? = null, val title: String? = null, val source: SourceKind)
enum class SourceKind { PAGE_MEDIA, YT_DLP, HLS_MANIFEST, DASH_MANIFEST, DIRECT_FILE }
data class MediaFormat(val formatId: String, val label: String, val height: Int? = null, val width: Int? = null, val videoCodec: String? = null, val audioCodec: String? = null, val container: String? = null, val estimatedBytes: Long? = null)
sealed interface ProbeResult {
    data class Formats(val items: List<MediaFormat>) : ProbeResult { init { require(items.isNotEmpty()) } }
    data class DirectDownload(val candidate: MediaCandidate) : ProbeResult
    data class Unavailable(val reason: String) : ProbeResult
}
interface MediaProbe { suspend fun probe(candidate: MediaCandidate): ProbeResult }
interface DownloadBackend { suspend fun enqueue(candidate: MediaCandidate, format: MediaFormat? = null): String }

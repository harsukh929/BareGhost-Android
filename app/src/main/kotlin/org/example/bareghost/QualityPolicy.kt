package org.example.bareghost

sealed interface DownloadUi {
    data object Hidden : DownloadUi
    data object Probing : DownloadUi
    data class QualityChoices(val formats: List<MediaFormat>) : DownloadUi
    data object GenericDownload : DownloadUi
    data class Unavailable(val message: String) : DownloadUi
}
fun ProbeResult.toDownloadUi(): DownloadUi = when (this) {
    is ProbeResult.Formats -> DownloadUi.QualityChoices(items)
    is ProbeResult.DirectDownload -> DownloadUi.GenericDownload
    is ProbeResult.Unavailable -> DownloadUi.Unavailable(reason)
}

package org.example.bareghost

import java.net.URI

/**
 * Narrow, explicit hand-off from the browser to an Android downloader host.
 *
 * This is a contract only: it does not start a download until a concrete
 * Ghost Android runtime implementation is connected.
 */
data class DownloadRequest(
    val pageUrl: String,
    val mediaUrl: String,
    val title: String?,
    val formatId: String?,
    val headers: Map<String, String> = emptyMap(),
    val isIncognito: Boolean = false,
    val allowSessionCookies: Boolean = false
) {
    init {
        require(isHttpUrl(pageUrl)) { "Page URL must be HTTP(S)." }
        require(isHttpUrl(mediaUrl)) { "Media URL must be HTTP(S)." }
        require(!(isIncognito && allowSessionCookies)) {
            "Incognito requests must never forward session cookies."
        }
        headers.forEach { (name, value) ->
            require(name.isNotBlank() && name.none { it == '\r' || it == '\n' }) {
                "Invalid HTTP header name."
            }
            require(value.none { it == '\r' || it == '\n' }) {
                "Invalid HTTP header value."
            }
            if (!allowSessionCookies) {
                require(!name.equals("cookie", ignoreCase = true) &&
                    !name.equals("cookie2", ignoreCase = true)) {
                    "Cookie headers require explicit user permission."
                }
            }
        }
    }

    companion object {
        private fun isHttpUrl(value: String): Boolean = try {
            val uri = URI(value)
            (uri.scheme.equals("http", true) || uri.scheme.equals("https", true)) &&
                !uri.host.isNullOrBlank()
        } catch (_: Exception) {
            false
        }
    }
}

/** Implemented by the Android host once the Ghost runtime/API is available. */
interface DownloaderHost {
    suspend fun probe(request: DownloadRequest): ProbeResult
    suspend fun enqueue(request: DownloadRequest, format: MediaFormat? = null): String
}

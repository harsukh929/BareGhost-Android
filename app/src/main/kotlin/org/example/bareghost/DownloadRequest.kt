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
        require(title == null || title.length <= MAX_TITLE_LENGTH) {
            "Title is too long."
        }
        require(formatId == null || formatId.length <= MAX_FORMAT_ID_LENGTH) {
            "Format ID is too long."
        }
        require(headers.size <= MAX_HEADERS) { "Too many HTTP headers." }
        require(!(isIncognito && allowSessionCookies)) {
            "Incognito requests must never forward session cookies."
        }
        headers.forEach { (name, value) ->
            require(HEADER_NAME.matches(name)) { "Invalid HTTP header name." }
            require(value.length <= MAX_HEADER_VALUE_LENGTH) {
                "HTTP header value is too long."
            }
            require(value.none { it == '\\r' || it == '\\n' }) {
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
        private const val MAX_HEADERS = 64
        private const val MAX_HEADER_VALUE_LENGTH = 8192
        private const val MAX_TITLE_LENGTH = 512
        private const val MAX_FORMAT_ID_LENGTH = 128
        private val HEADER_NAME =
            Regex("^[!#$%&'*+.^_`|~0-9A-Za-z-]+$")

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

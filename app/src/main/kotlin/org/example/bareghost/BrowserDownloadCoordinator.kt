package org.example.bareghost

import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch
import java.net.URI
import java.util.concurrent.atomic.AtomicLong

/**
 * Connect this coordinator to Bare/Chromium's native download callback.
 *
 * The browser callback must be invoked for an explicit user download action
 * (or a browser download event). The coordinator forwards the URL directly
 * to the injected Ghost-backed DownloaderHost; it does not open another app
 * and does not ask the user to copy/paste a link.
 *
 * This class is the in-process integration seam. A real Ghost Android host
 * implementation must still be supplied through DownloaderHost.
 */
class BrowserDownloadCoordinator(
    private val scope: CoroutineScope,
    private val downloader: DownloaderHost,
    private val listener: Listener
) {
    private val ids = AtomicLong(0)

    interface Listener {
        fun onStarted(requestId: String, ghostTaskId: String)
        fun onFailed(requestId: String, reason: String)
    }

    /**
     * Call from Bare's download-start callback with the original HTTP(S) URL.
     * Do not call for DRM license, segment-key, or other protected endpoints.
     */
    fun onBrowserDownload(
        url: String,
        pageUrl: String,
        suggestedFileName: String?,
        headers: Map<String, String> = emptyMap(),
        isIncognito: Boolean = false
    ): String {
        val requestId = "browser-download-${ids.incrementAndGet()}"
        val request = try {
            DownloadRequest(
                pageUrl = pageUrl,
                mediaUrl = url,
                title = suggestedFileName?.take(512),
                formatId = null,
                headers = headers,
                isIncognito = isIncognito,
                allowSessionCookies = false
            )
        } catch (error: IllegalArgumentException) {
            listener.onFailed(requestId, error.message ?: "Invalid download request.")
            return requestId
        }

        scope.launch {
            try {
                val ghostTaskId = downloader.enqueue(request, format = null)
                listener.onStarted(requestId, ghostTaskId)
            } catch (error: Exception) {
                listener.onFailed(
                    requestId,
                    error.message ?: "Ghost Downloader could not start this download."
                )
            }
        }
        return requestId
    }

    /**
     * Optional helper for browser callbacks that may deliver non-web schemes.
     * Only HTTP and HTTPS URLs are handed to Ghost.
     */
    companion object {
        fun isSupportedDownloadUrl(value: String): Boolean = try {
            val uri = URI(value)
            (uri.scheme.equals("http", true) || uri.scheme.equals("https", true)) &&
                !uri.host.isNullOrBlank()
        } catch (_: Exception) {
            false
        }
    }
}

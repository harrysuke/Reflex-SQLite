"""Reflex application configuration."""
import reflex as rx

config = rx.Config(
    app_name="reflexsqlite",
    frontend_port=3000,
    backend_port=8000,
    telemetry_enabled=False,
    # Declare plugins explicitly: avoids the implicit-Radix and default-Sitemap
    # deprecation warnings emitted by Reflex 0.10.x at startup.
    plugins=[rx.plugins.RadixThemesPlugin()],
    disable_plugins=[rx.plugins.SitemapPlugin],
)

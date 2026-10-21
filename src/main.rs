use graffalo_agent_bridge::Bridge;
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut origin = "https://graffalo.io".to_string();
    let mut port = 43781u16;
    let mut args = std::env::args().skip(1);
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--origin" => {
                origin = args
                    .next()
                    .ok_or("--origin needs the exact Graffalo origin")?
            }
            "--port" => {
                port = args.next().ok_or("--port needs a number")?.parse()?;
                if port == 0 {
                    return Err("Choose a fixed local port".into());
                }
            }
            "--version" | "-V" => {
                println!(
                    "graffalo-agent-bridge {} (protocol {})",
                    env!("CARGO_PKG_VERSION"),
                    graffalo_agent_bridge::PROTOCOL_VERSION
                );
                return Ok(());
            }
            "--licenses" => {
                println!(
                    "{}\n{}",
                    include_str!("../LICENSE"),
                    include_str!("../THIRD_PARTY_NOTICES.txt")
                );
                return Ok(());
            }
            "--help" | "-h" => {
                println!(
                    "graffalo-agent-bridge [--origin https://graffalo.io] [--port 43781]\nOptions: --version, --licenses, --help\nRequires an installed, signed-in Codex or Grok Build. Pairing expires on exit or after six hours."
                );
                return Ok(());
            }
            _ => return Err("Unknown option; use --help".into()),
        }
    }
    let bridge = Bridge::new(origin.clone(), port)?;
    let listener = tokio::net::TcpListener::bind((std::net::Ipv4Addr::LOCALHOST, port)).await?;
    println!(
        "Graffalo local agent companion\nEditor: {origin}\nCompanion port: {port}\nSession pairing code: {}\nPaste this code into Graffalo → Agent chat. Keep this terminal running.\nNo provider API keys or passwords are collected.",
        bridge.pairing_code()
    );
    axum::serve(listener, bridge.router())
        .with_graceful_shutdown(async {
            let _ = tokio::signal::ctrl_c().await;
        })
        .await?;
    Ok(())
}

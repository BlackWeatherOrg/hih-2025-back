local.file_match "applogs" {
    path_targets = [{"__path__" = env("LOGS_PATH")}]
}

loki.source.file "local_files" {
    targets    = local.file_match.applogs.targets
    forward_to = [loki.write.global.receiver]
}

loki.write "global" {
  endpoint {
    url = env("GRAFANA_URL")
  }
}

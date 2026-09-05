// Query all SOLCANCELAMENTO records
query solcancelamento verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $solcancelamento
  }

  response = $solcancelamento
  guid = "12rVUx-GUtpuBbViECK6PdmzicM"
}
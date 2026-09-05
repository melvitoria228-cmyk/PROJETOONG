// Query all STATUS_TRANSACAO records
query status_transacao verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $status_transacao
  }

  response = $status_transacao
  guid = "ICgPuXeAPMA1DIX-Gnd5-zuEUZU"
}
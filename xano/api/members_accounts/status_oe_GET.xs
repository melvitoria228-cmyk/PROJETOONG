// Query all STATUS_OE records
query status_oe verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $status_oe
  }

  response = $status_oe
  guid = "DSsg6rWw4uvcEk2uiVbb3psXD4E"
}
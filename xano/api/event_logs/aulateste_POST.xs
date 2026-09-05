// Add AulaTeste record
query aulateste verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $aulateste
  }

  response = $aulateste
  guid = "jJSX4O5O2lhC7Zu4dwsHsVYsN6g"
}
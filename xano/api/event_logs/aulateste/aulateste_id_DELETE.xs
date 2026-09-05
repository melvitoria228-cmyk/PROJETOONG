// Delete AulaTeste record.
query "aulateste/{aulateste_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int aulateste_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.aulateste_id
    }
  }

  response = null
  guid = "Y4ieusYZ8yWGQxmaSnHOYkhQCRo"
}
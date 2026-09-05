// Get AulaTeste record
query "aulateste/{aulateste_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int aulateste_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.aulateste_id
    } as $aulateste
  
    precondition ($aulateste != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $aulateste
  guid = "HU9aHxJ0alDZ2FWo4Gv4m12qQm0"
}
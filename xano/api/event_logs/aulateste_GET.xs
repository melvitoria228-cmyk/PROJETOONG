// Query all AulaTeste records
query aulateste verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $aulateste
  }

  response = $aulateste
  guid = "okjbzU2kvQY8msSTqvqO5xa9SnU"
}
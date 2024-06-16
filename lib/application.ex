defmodule VenomousExamples.Application do
  use Application

  def start(_type, _args) do
    children = [
      {Venomous.SnakeSupervisor, [strategy: :one_for_one, max_restarts: 0, max_children: 50]},
      {Venomous.PetSnakeSupervisor, [strategy: :one_for_one, max_children: 10]}
    ]

    opts = [strategy: :one_for_one, name: VenomousExamples.Supervisor]
    Supervisor.start_link(children, opts)
  end
end

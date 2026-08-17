TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_sum",
            "description": (
                "Perform a mathematical operation on two numbers. "
                "Supported operations are sum, subtract, multiply, "
                "divide, and floor_division."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "The first number"
                    },
                    "b": {
                        "type": "integer",
                        "description": "The second number"
                    },
                    "expression": {
                        "type": "string",
                        "enum": [
                            "sum",
                            "subtract",
                            "multiply",
                            "divide",
                            "floor_division"
                        ],
                        "description": (
                            "The mathematical operation to perform."
                        )
                    }
                },
                "required": [
                    "a",
                    "b",
                    "expression"
                ]
            }
        }
    }
]
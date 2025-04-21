# Stupid Watch

A simple and efficient command-line stopwatch tool for tracking time spent on different sessions.

## Features

- 🕒 Start and track multiple stopwatch sessions
- 📊 View total time spent on each session
- 🗑️ Delete sessions when no longer needed
- 🖥️ Create paired tmux sessions for continuous time tracking

## Installation

```bash
git clone https://github.com/MrMoneyInTheBank/stupid-watch.git
pipx install --editable .
```

## Usage

### Basic Commands

Start a new stopwatch session:
```bash
watch start my-session
```

List all sessions and their total times:
```bash
watch sessions
```

Delete a specific session:
```bash
watch delete-session my-session
```

### Advanced Usage

Create a paired tmux and watch session:
```bash
watch create-watch-tmux-session my-session
```

## Requirements

- Python 3.11 or higher
- Click
- Rich

## License

This project is licensed under the terms of the LICENSE file in the root of this repository.
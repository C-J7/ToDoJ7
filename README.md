### TODO_J7

# Todo List Application

A Todo List application with a Python GUI and REST API backend.


## Features

- 🖥 Modern dark theme UI
- ✅ Add/Edit/Delete todos
- ☑ Toggle completion status
- 📱 Responsive design
- 🔄 Real-time API synchronization
- 🛠 Error handling and validation
- 📜 Scrollable todo list

## Tech Stack

- **Frontend**: Tkinter (Python GUI)
- **Backend**: Flask (Python REST API)
- **Communication**: HTTP REST API

## Requirements
- Python 3.6+
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/
cd todo-app
```

2. Install dependencies:
```bash
pip install flask requests flask-cors
```

## Running the Application

1. Start the API server (in one terminal):
```bash
python todo_api.py
```

2. Start the GUI client (in another terminal):
```bash
python todo_gui.py
```
            

## Application Structure

todo-app/
├── todo_api.py      # Flask API server
├── todo_gui.py      # Tkinter GUI client
└── README.md        # Documentation


## Key Features Implementation

- **Dark Theme**: Custom Tkinter styling with contrast colors
- **Scrollable List**: Canvas-based scrollable container
- **Real-time Sync**: Automatic refresh after API operations
- **Error Handling**: Connection error detection and user feedback

## Future Improvements

- [ ] Add due dates and priority levels
- [ ] Implement data persistence with database
- [ ] Add user authentication
- [ ] Add category/tag system
- [ ] Export/Import functionality

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss proposed changes.

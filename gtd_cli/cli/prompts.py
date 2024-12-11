import questionary


def capture_inbox_item():
    """Capture a single inbox item interactively."""
    while True:
        title = questionary.text("Title: ", qmark="").ask()
        
        if title is None:
            return None
            
        if not title:
            choice = questionary.select(
                "Title cannot be empty. What would you like to do?",
                choices=[
                    "Enter title again",
                    "Abandon capture"
                ],
                qmark=""
            ).ask()
            
            if choice == "Abandon capture":
                return None
            continue 
    
        description = capture_description()
        if description is None:
            return None
        
        return {
            "title": title,
            "description": description or "",
        }

def capture_description():
    """Capture a multi-line description from user input."""
    print("Enter description (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if not line and (not lines or not lines[-1]):
            break
        lines.append(line)
    return '\n'.join(lines).rstrip()

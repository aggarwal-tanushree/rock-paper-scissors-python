# Rock, Paper, Scissors Game Flow Diagram

```mermaid
flowchart TD
    A[Game Start] --> B[Menu Screen]
    B -->|Click "Enter Your Name"| C[Name Input Screen]
    C -->|Type name & Click "Start Game"| D[Playing Screen]
    D -->|Select Rock/Paper/Scissors| E[Result Screen]
    
    E -->|Click "Play Again" or Press Y| D
    E -->|Click "End Game" or Press N| F[End Screen]
    
    F -->|Click "Restart" or Press R| B
    F -->|Click "Quit" or Press Q| G[Game Exit]
    
    %% Game state descriptions
    subgraph States
        B[Menu Screen<br>- Show game title<br>- Show enter name button]
        C[Name Input Screen<br>- Text input for player name<br>- Start game button]
        D[Playing Screen<br>- Show player name<br>- Display Rock/Paper/Scissors options]
        E[Result Screen<br>- Show player & computer choices<br>- Display winner<br>- Update scores<br>- Show play again/end options]
        F[End Screen<br>- Show final scores<br>- Display game outcome<br>- Show restart/quit options]
    end
    
    %% Game logic
    subgraph Logic
        H[Determine Winner<br>- Rock beats Scissors<br>- Scissors beat Paper<br>- Paper beats Rock]
        D -->|Make choice| H
        H --> E
    end
```
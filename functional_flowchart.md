```mermaid
graph TD
    MainPage((Main Page)) --> Sidebar[Choose from Sidebar]
    
    Sidebar -->|Insertion| Insertion[Insertion Tab]
    Sidebar -->|Viewing| Viewing[Viewing Tab]
    Sidebar -->|More Options| MoreOptions[More Options Tab]
    
    %% Insertion Path
    Insertion --> AddClient[Add a Client]
    AddClient --> AddProject[Add a Project (after Client)]
    
    %% Viewing Path
    Viewing --> ViewClient[View Clients]
    Viewing --> ViewProjects[View Projects]
    ViewProjects --> TaskTable[Display Task Table]
    
    %% More Options Path
    MoreOptions --> EditOptions[Edit]
    MoreOptions --> ArchiveOptions[Archive]
    MoreOptions --> DeleteOptions[Delete]
    
    %% Edit Path
    EditOptions -->|Client| EditClient[Edit Client Details]
    EditOptions -->|Project| EditProject[Edit Project Details]
    
    %% Archive Path
    ArchiveOptions -->|Archive| ArchiveAction[Archive Client/Project]
    ArchiveOptions -->|Unarchive| UnarchiveAction[Unarchive Client/Project]
    
    %% Delete Path
    DeleteOptions -->|Client| DeleteClient[Delete a Client]
    DeleteOptions -->|Project| DeleteProject[Delete a Project]

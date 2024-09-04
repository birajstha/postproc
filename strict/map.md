```mermaid
flowchart TD
    A[All subject Output dir] --> B[all files in func with space-MNI in filename]
    B --> C[Run 3dresample to RPI]
    C --> D[All files with space-MNI and ending with _bold]
    D --> E[Change pixdim4 to TR value 0.8]
    E --> F[All files with reg- in filename]
    F --> G[Perform spike regression operations]
    G --> H[Grab the regressor]
    H --> I[Run the inverting function]
    I --> J[Apply 3dTproject with the spike regressor]
    J --> K[End]
import json
from pathlib import Path
from typing import Any

class Memory:

    def __init__(self, file_path: str | Path):

        self.file_path = Path(file_path) #dónde está el archivo de memoria
        self.data: dict[str, Any] = {} #qué hay en el archivo
        self.load()

    def load(self) -> None:
        """
        Carga la memoria desde el archivo JSON.
        
        Si el archivo o su carpeta no existen, los crea.
        """

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.file_path.exists():
            self.save_to_disk()
            return

        try:
            with self.file_path.open(
                mode="r",
                encoding="utf-8"
            ) as file:
                loaded_data = json.load(file)
        
        except json.JSONDecodeError as error:
        
            raise ValueError(
                f"El archivo de memoria no contiene JSON válido: "
                f"{self.file_path}"
            ) from error

        if not isinstance(loaded_data, dict):

            raise ValueError(
                "El contenido del archivo de memoria debe ser "
                "un objeto JSON."
            )
    
        self.data = loaded_data

    def save_to_disk(self) -> None:
        """
        Guarda el contenido actual de self.data en el archivo JSON.
        """

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with self.file_path.open(
            mode="w",
            encoding="utf-8"
        ) as file:
            
            json.dump(
                self.data,
                file,
                ensure_ascii=False,
                indent=4
            )

    def get(
            self,
            key: str,
            default: Any = None
    ) -> Any:
        """
        Devuelve el valor asociado a una clave.

        Si no existe, devuelve default.
        """        

        return self.data.get(key, default)
    
    def save(
            self,
            key: str,
            value: Any
    ) -> None:
        """
        Guarda una memoria nueva.

        Lanza KeyError si la clave ya existe.
        """

        if key in self.data:

            raise KeyError(
                f"La memoria '{key}' ya existe."
            )
        
        self.data[key] = value

        self.save_to_disk()

    def update(
            self,
            key: str,
            value: Any
    ) -> None:
        """
        Actualiza una memoria existente.

        Lanza KEyError si la clave no existe.        
        """

        if key not in self.data:

            raise KeyError(
                f"La memoria '{key}' no existe."
            )
        
        self.data[key] = value

        self.save_to_disk()

    def delete(self, key: str) -> None:
        """
        Elimina una memoria existente.

        Lanza KeyError si la clave no existe.
        """

        if key not in self.data:

            raise KeyError(
                f"La memoria '{key}' no existe."
            )
        
        del self.data[key]

        self.save_to_disk()

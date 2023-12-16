from typing import Any

class Unbuffered:
   def __init__(self, stream) -> None:
       self.stream = stream

   def write(self, data) -> None:
       self.stream.write(data)
       self.stream.flush()

   def writelines(self, datas) -> None:
       self.stream.writelines(datas)
       self.stream.flush()

   def __getattr__(self, attr) -> Any:
       return getattr(self.stream, attr)

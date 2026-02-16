"""
UseCase Interface for Clean Architecture.
All use cases must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic


InputDTO = TypeVar('InputDTO')
OutputDTO = TypeVar('OutputDTO')


class UseCase(ABC, Generic[InputDTO, OutputDTO]):
    """
    Abstract base class for all use cases.
    
    Use cases represent the rules of the application that orchestrate
    the flow of data to and from the entities while fulfilling a specific
    business goal.
    
    According to Clean Architecture:
    - Use cases are the second innermost layer
    - They contain application-specific business rules
    - They should be independent of frameworks and external details
    - They orchestrate entities to achieve business objectives
    """
    
    @abstractmethod
    def execute(self, input_dto: InputDTO) -> OutputDTO:
        """
        Execute the use case logic.
        
        Args:
            input_dto: Data Transfer Object containing input data
            
        Returns:
            OutputDTO: Data Transfer Object containing result data
        """
        pass

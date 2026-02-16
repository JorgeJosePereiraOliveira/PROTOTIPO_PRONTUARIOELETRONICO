"""
Repository Interface for Clean Architecture.
All repositories must implement this interface.
Repositories are adapters that decouple the domain layer from persistence details.

Propósito:
Definine um contrato abstrato que todos os repositórios devem seguir. Um 
repositório é um adaptador que desacopla a camada de domínio dos detalhes de 
persistência (banco de dados, cache, arquivo, etc.).

Benefício: A camada de domínio só conhece a interface, não sabe qual banco de 
dados está sendo usado.

Vantagens:
Flexibilidade: Trocar banco de dados sem alterar código de domínio
Testabilidade: Criar mock repositories para testes
Desacoplamento: Domínio não depende de implementações concretas
Escalabilidade: Múltiplas implementações (SQL, NoSQL, cache, etc.)
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

from .entity import Entity


Entity_T = TypeVar('Entity_T', bound=Entity)


class RepositoryInterface(ABC, Generic[Entity_T]):
    """
    Abstract base class for all repository interfaces.
    
    Repositories define the contract for persisting and retrieving entities.
    They act as an abstraction layer between the application and the data
    persistence mechanism (database, cache, file system, etc.).
    
    According to Clean Architecture:
    - Repository interfaces are defined in the Application/Use Cases layer
    - Concrete implementations are in the Frameworks & Drivers layer
    - This inversion of dependency ensures inner layers don't depend on outer layers
    """
    
    @abstractmethod
    def add(self, entity: Entity_T) -> None:
        """
        Add/save a new entity to the repository.
        
        Args:
            entity: The entity to add
            
        Raises:
            Exception: If entity already exists or save fails
        """
        pass
    
    @abstractmethod
    def update(self, entity: Entity_T) -> None:
        """
        Update an existing entity in the repository.
        
        Args:
            entity: The entity to update
            
        Raises:
            Exception: If entity not found or update fails
        """
        pass
    
    @abstractmethod
    def delete(self, id: str) -> None:
        """
        Delete an entity from the repository.
        
        Args:
            id: The ID of the entity to delete
            
        Raises:
            Exception: If entity not found or delete fails
        """
        pass
    
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Entity_T]:
        """
        Find an entity by its ID.
        
        Args:
            id: The ID of the entity
            
        Returns:
            Optional[Entity_T]: The entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[Entity_T]:
        """
        Find all entities in the repository.
        
        Returns:
            List[Entity_T]: List of all entities
        """
        pass

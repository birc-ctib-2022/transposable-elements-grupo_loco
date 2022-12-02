"""A circular genome for simulating transposable elements."""
from __future__ import annotations
from typing import (
    Generic, TypeVar, Iterable,
    Callable, Protocol)

from abc import (
    # A tag that says that we can't use this class except by specialising it
    ABC,
    # A tag that says that this method must be implemented by a child class
    abstractmethod
)


class Genome(ABC):
    """Representation of a circular enome."""

    def __init__(self, n: int):
        """Create a genome of size n."""
        ...  # not implemented yet
    

    @abstractmethod
    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        ...  # not implemented yet
    

    @abstractmethod
    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        ...  # not implemented yet

    @abstractmethod
    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # not implemented yet

    @abstractmethod
    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        ...  # not implemented yet

    @abstractmethod
    def __len__(self) -> int:
        """Get the current length of the genome."""
        ...  # not implemented yet

    @abstractmethod
    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        ...  # not implemented yet


class ListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using Python's built-in lists
    """
    def __init__(self, n: int):
        """Create a new genome with length n."""
        ...  # FIXME
        self.genome=['-']*n
        self.tes = {}
        self.inactive = set()
        self.counter=0

    

    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        ...  # FIXME
  
        if self.genome[pos] == 'A':
            self.disable_te(self.tes[pos])
        self.genome[pos] = 'A'
        self.tes[pos] = self.counter
        self.counter += 1
        return self.counter - 1

    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """

        for i in range(len(self.genome)): #find the position of the te
            if self.tes[i] == te:
                pos = i #position of the te
        if pos + offset < 0: #if the offset moves the copy left of index 0
            pos = len(self.genome) + (pos + offset)
        elif pos + offset > len(self.genome): #if the offset moves the copy right of the largest index
            pos = pos + offset - len(self.genome)
        else:
            pos = pos + offset
        if self.genome[pos] == 'A': #if the te collides with an existing te
            self.disable_te(self.tes[pos])  #disable the te if it is active and add it to the inactive set
        if te in self.tes.values(): #if te is active   
            self.genome[pos] = 'A' #copy the te to the new position
        #if the te collides with an existing te, disable the te and add it to the inactive set
        #if te is not active, return None (and do not copy it)
        return self.counter - 1
    


            

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # FIXME
        for i in range(len(self.genome)):
            if self.tes[i] == te:
                pos = i #position of the te to be disabled
        if te in self.tes.values(): #if te is active
            self.genome[pos] = 'x' #disable the te
            self.inactive.add(te) #add the te to the inactive set
        else:
            return None


    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        ...  # FIXME
        active = []
        for i in range(len(self.genome)):
            if self.genome[i] == 'A':
                active.append(self.tes[i])
        return active


    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        ...
        return ''.join(self.genome)



T = TypeVar('T')
S = TypeVar('S')

class Link(Generic[T]):
    """Doubly linked link."""

    val: T
    prev: Link[T]
    next: Link[T]

    def __init__(self, val: T, p: Link[T], n: Link[T]):
        """Create a new link and link up prev and next."""
        self.val = val
        self.prev = p
        self.next = n


def insert_after(link: Link[T], val: T) -> None:
    """Add a new link containing avl after link."""
    new_link = Link(val, link, link.next)
    new_link.prev.next = new_link
    new_link.next.prev = new_link


def remove_link(link: Link[T]) -> None:
    """Remove link from the list."""
    link.prev.next = link.next
    link.next.prev = link.prev        


class LinkedListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using linked lists.
    """


    def __init__(self, n: int):
        """Create a new genome with length n."""
        ...  # FIXME
        self.head = Link(None, None, None)  # type: ignore
        self.head.prev = self.head
        self.head.next = self.head

        self.inactive=set()
        self.tes=set()

        for _ in range(n):
            insert_after(self.head,'-')
       

    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        ...  # FIXME
        Curro=self.head.next
        Curros=self.head.prev
        counter=0
        for points in Curro:
            if  counter >= pos and counter<=pos+length and points!='-':
                self.inactive.add(points)
                Curro.val='x'
                counter+=1
                Curro=Curro.next
            counter+=1
            Curro=Curro.next
            if Curro==Curros:
                return
        self.tes.add(len(self.tes))
        
        Churro=self.head.next
        count=0
        Churros=self.head.prev
        for ele in Churro:
            if count >= pos-1 and count<=pos+length-1:
                insert_after(Churro.val, len(self.tes))
                count+=1
                Churro=Churro.next
            count+=1
            if Churros==Churro:
                return
            Churro=Churro.next


    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        ...  # FIXME
        Churro=self.head.next
        count=0
        Churros=self.head.prev

        if te in self.inactive:
            return None

        for ele in Churro:
            if count==offset:
                insert_after(ele,te+offset)
                break
            count+=1
            if Churros==Churro:
                break
            Churro=Churro.next
    

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # FIXME
        Churro=self.head.next

        for elements in Churro:
            if elements==te:
                self.inactive.add(te)
                self.tes.remove(te)
                Churro.val='x'
                Churro=Churro.next
            Churro=Churro.next
            if Churro==self.head.prev:
                break
         

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        # FIXME
        return self.tes

    def __len__(self) -> int:
        """Current length of the genome."""
        # FIXME
        count=0
        Curro=self.head.next
        for _ in Curro:
            count+=1
            Curro=Curro.next
            if Curro==self.head.prev:
                break
        return count

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        string_curro = []
        Curro = self.head.next
        for elements in Curro:
            if elements==int:
                string_curro.append('A')
                Curro=Curro.next
            string_curro.append(Curro.val) 
            Curro==Curro.next
            if Curro==self.head.prev:
                break  

        ''.join(string_curro)
        return string_curro

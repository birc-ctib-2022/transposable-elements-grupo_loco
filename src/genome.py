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
        self.genome=[0]*n
        self.tes =set()
        self.counter=1

    

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
        if self.genome[pos] in self.tes:
            self.tes.remove(self.genome[pos])

        te=self.counter
        self.tes.add(te)
        self.counter+=1
        self.genome[pos:pos] = [te]*length

        return te
        


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
        counter0=-1
        for i in self.genome:
            counter0+=1
            if i==te:
                break

        if te not in self.tes:
            return None

        counter=0
        for i in self.genome:#to find the length of the te
            if i==te:
                counter+=1
        return self.insert_te((counter0+offset)%len(self.genome),counter) # adding the offset since the number need to change accordingly
        #the Modulos is so it will wrap around.
      


            

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # FIXME
    
        if te in self.tes:
            self.tes.remove(te)
    

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        ...  # FIXME
        return list(self.tes)


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
        return ''.join("-" if nuc==0 else "A" if nuc in self.tes else "x"
                        for nuc in self.genome)


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

def insert_before(link: Link[T], val: T) -> None:
    """Add a new link before containing avl of link."""
    new_link = Link(val, link.prev, link)
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
        self.counter = 1

        self.tes=set()

        for _ in range(n):
            insert_after(self.head,0)
       

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
        counter=-1

        while Curro is not self.head:
            if  counter==pos and Curro.val>0:
                self.tes.remove(Curro.val)
                counter+=1
                break
            counter+=1
            Curro=Curro.next

        te=self.counter
        self.tes.add(te)
        
        self.counter+=1

        Churro=self.head.next
        count=1
        while Churro is not self.head:#this one we insert the genome from pos until pos+length
            if count >= pos and count<pos+length:
                insert_after(Churro, te)
                count+=1
                Churro=Churro.next
            else:
                count+=1
                Churro=Churro.next
        
        return te

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
        
        
        if te in self.tes:
            return None
        
        Burro=self.head.next
        Countings=0

        while Burro is not self.head:
            Countings+=1
            Burro=Burro.next
        
        Churro=self.head.next
        count=0

        while Churro is not self.head:
            if count==offset:
                insert_after(count,(te+offset)%Countings)
                break
    
            else:
                Churro=Churro.next
                count+=1

    

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # FIXME
        Churro=self.head.next

        while Churro is not:
            if Churro.val==te:
                self.tes.remove(te)
                Churro.val='x'
                Churro=Churro.next
            Churro=Churro.next
            if Churro==self.head.prev:
                break
         

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        # FIXME
        return list(self.tes)

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
        while Curro is not self.head:
            if Curro.val==0:
                string_curro.append('-')
                Curro=Curro.next

            elif Curro.val>0 and Curro.val not in self.tes:
                string_curro.append('x')
                Curro=Curro.next

            elif Curro.val>0:
                string_curro.append('A')
                Curro=Curro.next


           
        
        return ''.join(string_curro)

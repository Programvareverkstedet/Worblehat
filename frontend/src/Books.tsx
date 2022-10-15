import React from 'react';
import Book from './components/Book';
import { useEffect } from 'react';

function BooksPage() {
    const [books, setBooks] = React.useState<string[]>([]);
    useEffect(() => {
        setBooks(["The Hobbit", "The Lord of the Rings", "The Silmarillion"]); 
    }, []);
    
    return (
        <div>
            <h1>
                Books Page!
            </h1>
            <ul>
                {books.map((title) => <Book title={title} />)}
            </ul>
        </div>
        );
    }
    
    export default BooksPage;

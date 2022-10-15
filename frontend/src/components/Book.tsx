import React from 'react';

interface BookProps {
    title: string;
}
function Book(props: BookProps) {
    return (
        <li>
          {props.title}
        </li>
    );
  }
  
  export default Book;
  
//////////////////////////  iMPORTING all THE required Liraries ////////////////


import { Flex, Box, Text, Heading, VStack, Button } from '@chakra-ui/react';
import { Input} from '@chakra-ui/react'
import React, {useState, useEffect} from 'react';
import axios from 'axios'
import ReactPaginate from 'react-paginate';


///////////////////////   Defining All the required variables //////////////////



function App() {
  const [data, setData]=useState(null);
  const [print, setPrint]= useState(false);
  const [show, setshow]= useState(false);
  const [posts, setPosts]= useState([]);


///////////////////////////   Data from my API ////////////////////

  useEffect(() => {
    const fetchPosts= async() => {
      const res=await axios({method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      url:"https://o3c5vdy44a.execute-api.us-east-2.amazonaws.com/prod/"});
      setPosts(res.data);
    }
    fetchPosts();
  },[]);

  const items = posts


  //////////////////////     Function to show urls from table ///////////////////////


function Items({ currentItems }) {
  return (
    <>
      {currentItems &&
        currentItems.map((item) => (
         
          <Box w='100%'>
          <Heading ml="2" size="md" >
          {item}
          </Heading>
          </Box> )
          )
        }
        </>  
  );
}



////////////////////////// function to Paginate the URLS /////////////////////

function PaginatedItems({ itemsPerPage }) 
{
  const [currentItems, setCurrentItems] = useState(null);
  const [pageCount, setPageCount] = useState(0);
  const [itemOffset, setItemOffset] = useState(0);

  useEffect(() => {
    const endOffset = itemOffset + itemsPerPage;
    console.log(`Loading items from ${itemOffset} to ${endOffset}`);
    setCurrentItems(items.slice(itemOffset, endOffset));
    setPageCount(Math.ceil(items.length / itemsPerPage));
  }, [itemOffset, itemsPerPage]);
  const handlePageClick = (event) => {
    const newOffset = (event.selected * itemsPerPage) % items.length;
    console.log(
      `User requested page number ${event.selected}, which is offset ${newOffset}`
    );
    setItemOffset(newOffset);
  };

  return (
    <VStack>
    <Flex>
    <Box>
      <Items currentItems={currentItems} />
      </Box>
    </Flex >
    <div > 
      <ReactPaginate
        breakLabel="..." nextLabel="Next>" 
        onPageChange={handlePageClick}
        pageRangeDisplayed={5}
        pageCount={pageCount}
        previousLabel="<Back"
        renderOnZeroPageCount={null}
      />

    </div>
    </VStack>
  );
}


//////////////////////////////// Function to search data from table //////////////////////

function getData(val)
{
  var d="";
  for (const el of items)
  {
    if (val.target.value === el)
    {
      d="Hurry!URL is found";
      break;
    }
    else
    {
      d="Sorry! The URL is not found";
    }
  }

  setData(d)
  setPrint(false)
  console.warn(val.target.value)
}



//////////////////////////// main return for app ////////////////////////////////


  return (
    <VStack >
      <Flex>
        <Heading> API WEB INTERFACE</Heading>
      </Flex>


      <Flex>
      <Box variant='outline' w='100%' p={2} color='black' >
        <Text fontSize ="2xl" fontWeight ="semibold"> Here you can search URL</Text>
      </Box>
      </Flex>


      <Flex>
      <Input mr ="3" placeholder='Enter URL to Search' type ="text" onChange={getData}/>      
      </Flex>
     <Flex> 
      <Button colorScheme='gray' onClick={()=> setPrint(true)} >
        Search </Button>
        </Flex>
        <Flex >
        { print?
        <Box variant='outline'  fontSize="1xl" p={2.5} color='blue.900' borderWidth='1px' borderRadius='lg' > {data} </Box>
        :null
        }
        </Flex>

        
         
        <Flex>
        </Flex> 
        <Flex>
      <Box variant='outline'  w='100%' p={2} color='black' >
        <Heading fontSize ="2xl" fontWeight ="semibold">Show Data</Heading>
      </Box>
      </Flex>
      <Flex>
      <Button  colorScheme='gray' onClick={(t)=>   setshow(true)    } >
        Display </Button>
       </Flex>
        <Flex>
        { show?
        <PaginatedItems itemsPerPage={2} />
        :null
        }
        </Flex>
  </VStack>

    );
}

export default App;
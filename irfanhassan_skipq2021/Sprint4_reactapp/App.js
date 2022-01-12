//************************************************************************************************** */
//   importing the classes from libraries wich are required for our React APP
import { IconButton } from "@chakra-ui/button";
import { Box, Button, Input } from "@chakra-ui/react";
import { useColorMode } from "@chakra-ui/color-mode";
import { Flex, VStack, Heading, Spacer } from "@chakra-ui/layout";
import { FaSun, FaMoon } from "react-icons/fa";
import React, { useState, useEffect} from 'react';
import axios from 'axios';
import ReactPaginate from 'react-paginate';

//************************************************************************************************* */
//       our Main Function start from here
function App() {

//creating some varibale and function to set variable value
  const [data, setdata] = useState(null)
  const [display, setdisplay] = useState(false)
  const [urllist, seturllist] = useState(false)
  const { colorMode, toggleColorMode } = useColorMode();
  const isDark = colorMode === "dark";
  const [posts, setPosts]= useState([]); 
  const [url, seturl]=useState(null) ;
  const apiurl="https://n0q8c9iur5.execute-api.us-east-2.amazonaws.com/prod/";
//*************************************************/
// fetching data, directly updating the URLS in item array
useEffect(() => {
  const fetchPosts= async() => {
    const res=await axios({method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    url:apiurl});
    setPosts(res.data);
  }
  fetchPosts();
},[]);
const items = posts
console.log(items)

//************************************************* */
// this function show URLs on current selected pages. 
function Items({ currentItems }) {
    return (
      <>
        {currentItems &&
         currentItems.map((item) => (
          <Box w='100%'>
          <Heading  color='white' ml="2" size="md" >
          {item}
          </Heading>
          </Box>
         ))}
        </>
      );
    }
//************************************************* */
//pagination function create pagination as well as define how many pages we need to display all urls and 
// also it fecth the urls for each page number and send to item function define above. 
    function PaginatedItems({ itemsPerPage }) 
    {
      const [currentItems, setCurrentItems] = useState(null);
      const [pageCount, setPageCount] = useState(0);
      const [itemOffset, setItemOffset] = useState(0);
    //************************************************************* */
    //continuosly getting the current page and display the array according to page is selcted by user
      useEffect(() => {
        const endOffset = itemOffset + itemsPerPage;
        console.log(`Loading items from ${itemOffset} to ${endOffset}`);
        setCurrentItems(items.slice(itemOffset, endOffset));
        setPageCount(Math.ceil(items.length / itemsPerPage));
      }, [itemOffset, itemsPerPage]);
    //**************************************************** */
    // this function allow user to click on pagination numeer and it updated offset vale 
      const handlePageClick = (event) => {
        const newOffset = (event.selected * itemsPerPage) % items.length;
        console.log(
          `User requested page number ${event.selected}, which is offset ${newOffset}`
        );
        setItemOffset(newOffset);
      };
    //******************************************************** */
    //pagnation will retun this ---display current url on selected page and add pagination number below the page.
      return (
        <VStack>
        <Flex>
        <Box bg='black' w='100%'>
          <Items currentItems={currentItems} />
          </Box>
        </Flex>
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
  //***************************************************** */
//function will store url enter by user 
function saveurl(event)
{
    var result=event.target.value;
    seturl(result)
    console.log(result)
    setdisplay(false)
    seturllist(false)
}
//************************************************************************ */
// this function enabe when user enter url to search and press search url button  
function searchdata() 
  {
    var result="";
    if (url==="")
    {
        result="Warning! Enter URL" ;
    }
    else
    {
      for (const element of items)
      {
       if (url===element)
       {
         result="URL exist in table";
         break;
       }
       else
       {
         result="URL not exist in table";
       }
      }
    }
    setdata(result)
    setdisplay(true)
  }
  //************************************************************************ */
  // this function enabe when user enter url to delete and press search delete url button
  function deletedata()
  {
    var result="";
    if (url==="")
    {
        result="Warning! Enter URL" ;
    }
    else
    {
      for (const element of items)
      {
       if (url===element)
       {
        axios.delete(apiurl, url)
        result="successfully deleted";
         break;
       }
       else
       {
         result="failed to delete:URL not exist in table";
       }
      }
    }
    setdata(result)
    setdisplay(true)
  }
  //************************************************************************ */
  // this function enabe when user enter url to add and press put url button
  function putdata()
  {
    var result="";
    var check=0;
    if (url==="")
    {
        result="Warning! Enter URL" ;
    }
    else
    {
      for (const element of items)
      {
       if (url===element)
       {
        result="failed to add:URL already exist in table";
        check =1;
         break;
       }
       else
       {
          result="successfully added URL to table";
       }
      }
      if (check==0)
      {
        axios.put(apiurl, url)
      }
    }
    setdata(result)
    setdisplay(true)
  }
  //************************************************************************ */
  // main function app is retunring this stack
  return (
    
  //  show my name and add icone button to toggle color mode for app
    <VStack>
      <Flex w="100%">
        <Heading ml="2" size="md" fontWeight='extrabold'
          color='blue.500' >M Irfan</Heading>
        <Spacer></Spacer>
        <IconButton ml={9} icon={isDark ? <FaSun /> : <FaMoon />}
          isRound="true" onClick={toggleColorMode}></IconButton>
      </Flex>
      <Flex w="30%">
        <Box bg='yellow' w='100%' p={4}>
          <Heading ml="2" size="md" fontWeight='extrabold'
            color='black' >CRUD API Gateway User Interface</Heading>  
        </Box>
      </Flex>

      <Flex w="30%">
        <Input type='text' variant='filled' placeholder='Enter URL' onChange={saveurl}/>
      </Flex>

      <Flex w='30%'>
        <Button colorScheme='green' size='lg' onClick={searchdata}>
          Search URL
        </Button>
        <Button colorScheme='yellow' size='lg' onClick={putdata}>
          Put URL
        </Button>
        <Button colorScheme='red' size='lg' onClick={deletedata}>
          Delete URL
        </Button>
      </Flex >

      <Flex w="100%">
        {
          display ?
            <Box bg='black' w='100%' p={4}><Heading ml="2" size="md"  color='white ' >{data}</Heading></Box>
            : null
        }

      </Flex>
      <Flex w='8%'>
        <Button colorScheme='blue' size='lg' onClick={()=>seturllist(true)}>
          Get URL 
        </Button>
      </Flex >

      <Flex w="100%">
        {
           urllist?
          <Box w="100%">           
            <PaginatedItems itemsPerPage={5} />
            </Box>
            : null
        }
      </Flex>
      
      

    </VStack>
  );
}
export default App;
//by default return APP. 
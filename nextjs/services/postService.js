import axios from "axios";
import buri from "../config/djangoBackend";
import token from "../config/userToken";

const PostService = () => {
  //   const config = { headers: { Authorization: `Bearer ${token}` } };
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  const likePost = async (postId) => {
    const url = `${buri}api/like/${postId}`;
    // const res = await axios({ method: "POST", url, config });
    const res = await axios.post(url);
    console.log(res.data);
    console.log(res);

    return res.data;
  };

  const getPost = async (postId) => {
    const url = `${buri}api/post/${postId}`;
    const res = await axios.get(url);
    console.log(res.data);
    return res.data;
  };

  const getLikes = async (postId) => {
    const url = `${buri}api/like/${postId}`;
    const res = await axios.get(url);
    console.log(res.data);
    return res.data;
  };

  const getComments = async (postId) => {
    const url = `${buri}api/post/comment/${postId}`;
    const res = await axios.get(url);
    console.log(res.data);
    return res.data;
  };

  return { likePost, getPost, getLikes, getComments };
};

export default PostService();

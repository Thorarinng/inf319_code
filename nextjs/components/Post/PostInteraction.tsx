import React, { useState, useEffect } from "react";
import {
  PersonCircle,
  Chat,
  ChatFill,
  Heart,
  HeartFill,
} from "react-bootstrap-icons";

import PostService from "../../services/postService";

import ps from "../../styles/Post.module.css";
import CreatePost from "./CreatePost";

export const PostInteraction = (props: { post: any; setPost: any }) => {
  const { post, setPost } = props;
  const { likeCount } = post;

  const [showComments, setShowComments] = useState(false);

  const [isLike, setIsLike] = useState(post.doesLike);

  const [likes, setLikes] = useState([]);
  const [comments, setComments] = useState([]);

  const [isLoading, setIsLoading] = useState(false);

  const likePost = async () => {
    if (isLoading) return;

    setIsLoading(true);
    setIsLike(!isLike);
    console.log(post);
    console.log(post.id);

    await PostService.likePost(post.id);
    const postData = await PostService.getPost(post.id);
    const likeData = await PostService.getLikes(post.id);

    console.log(likeData);

    setPost(postData.post);
    setLikes(likeData.likes);

    setIsLoading(false);
  };

  const getLikes = async () => {
    setIsLoading(true);
    const data = await PostService.getLikes(post.id);
    console.log(data.likes);
    setLikes(data.likes);
    setIsLoading(false);
  };

  const getComments = async () => {
    setIsLoading(true);
    const data = await PostService.getComments(post.id);
    setComments(data.childrenPosts);
    setIsLoading(false);
  };

  const showLikers = () => {
    console.log(post.likes);
    console.log(post.likes.length);
  };

  useEffect(async () => {
    await getLikes();
    await getComments();
  }, []);

  return (
    <div>
      {likes.length}
      {isLike ? (
        <HeartFill onClick={() => likePost()} className={ps.liked} />
      ) : (
        <Heart onClick={() => likePost()} className={ps.liked} />
      )}
      {/* like count on the post */}
      <span className="no-select">
        {likeCount > 0 ? (
          <span onClick={() => showLikers()}>{likeCount}</span>
        ) : (
          ""
        )}
      </span>
      {comments.length}
      {showComments ? (
        <>
          <ChatFill
            className={ps.liked}
            onClick={() => setShowComments(!showComments)}
          />
          <CreatePost />
        </>
      ) : (
        <Chat
          className={ps.like}
          onClick={() => setShowComments(!showComments)}
        />
      )}
    </div>
  );
};

import React, { useState } from "react";

import Link from "next/link";
import { PostHeader } from "./PostHeader";
import { PostContent } from "./PostContent";
import { PostInteraction } from "./PostInteraction";

import ps from "../../styles/Post.module.css";

export const Post = (props: { post: any }) => {
  // Get post from props
  const { post } = props;

  // Create hook instance with post data which enables us to mutate it
  const [p, setP] = useState(post);

  return (
    <>
      <div className={ps.container} key={post.user + post.date}>
        <PostHeader user={p.user} />
        <PostContent post={p} />
        <PostInteraction post={p} setPost={setP} />
      </div>
    </>
  );
};

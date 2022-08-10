import React from "react";
import { Post } from "./Post";

export const Posts = (props: { posts: any }) => {
  console.log("Posts");
  console.log(props.posts);
  const { posts } = props;
  return (
    <div>
      <h1>Posts</h1>
      <div>
        {posts.map((p: any) => (
          <Post key={p.id} post={p} />
        ))}
      </div>
    </div>
  );
};

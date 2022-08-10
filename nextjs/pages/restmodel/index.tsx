import type { NextPage } from "next";
import Head from "next/head";
import Image from "next/image";
import styles from "../../styles/Home.module.css";
import { Posts } from "../../components/Post/Posts";
import axios from "axios";
import Link from "next/link";

import { GetServerSideProps } from "next";
import { Followers } from "../../components/Follow/Followers";
import { Following } from "../../components/Follow/Following";

const Home: NextPage = (props: {
  posts: any;
  postTime: any;
  followers: any;
  followersTime: any;
  following: any;
  followingTime: any;
}) => {
  const {
    posts,
    postTime,
    followers,
    followersTime,
    following,
    followingTime,
  } = props;
  return (
    <div className={styles.container}>
      <div className={styles.threeWay}>
        <div className={styles.twChild}>
          <p>A</p>
        </div>
        <div className={styles.twChild}>
          <p>B</p>
          <Posts posts={posts} />
          {postTime} milliseconds
          <br />
          <br />
          <br />
          <button>
            <Link href="/">Home</Link>
          </button>
        </div>
        <div className={styles.twChild}>
          <p>C</p>
          <Followers followers={followers} />
          {followersTime} milliseconds
          <Following following={following} />
          {followingTime} milliseconds
        </div>
      </div>
    </div>
  );
};

const getLikes = async (p: any) => {
  // Gets user by userId
  const likeRes = await axios.get(`api/like/${p.id}`);
  p.likes = likeRes.data;
  return p;
};

const getPosts = async () => {
  // HTTP REQUESTS
  // -> api/posts
  // -> api/user/id/:userId
  // -> api/like/:postId

  const startTime = performance.now();
  console.log("Hello from 'getServerSideProps'");

  const res = await axios.get("api/post/");

  console.log("Server side");

  let { posts } = res.data;
  console.log("data");

  // posts = await Promise.all(posts.map(async (p: any) => getLikes(p)));

  console.log("newData");
  console.log(posts);

  const endTime = performance.now();

  return { posts, endTime, startTime };
};

const getFollowers = async () => {
  const startTime2 = performance.now();

  const res = await axios.get("api/follow/followers/");

  const { followers } = res.data;

  console.log("Followers");
  console.log(followers);

  const endTime2 = performance.now();

  return { followers, endTime2, startTime2 };
};

const getFollowing = async () => {
  const startTime3 = performance.now();

  const res = await axios.get("api/follow/following/");

  const { following } = res.data;

  console.log("Followers");
  console.log(following);

  const endTime3 = performance.now();

  return { following, endTime3, startTime3 };
};

export const getServerSideProps: GetServerSideProps = async (context) => {
  const token =
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYxNDIzMTIwLCJpYXQiOjE2NDk0MjMxMjAsImp0aSI6IjBjNTY3NzI1NjY3YzQwMmY5NjAzZGNkNTYwNjRkNzcwIiwidXNlcl9pZCI6MX0.uzGnzzLWsBs2ZS9IId2RmJg6jw7gYO1tUqP2LUuV5LM";
  axios.defaults.baseURL = "http://localhost:8000/";
  axios.defaults.headers.common = { Authorization: `bearer ${token}` };

  const { posts, endTime, startTime } = await getPosts();
  const { followers, endTime2, startTime2 } = await getFollowers();
  const { following, endTime3, startTime3 } = await getFollowing();

  return {
    props: {
      posts,
      postTime: endTime - startTime,
      followers,
      followersTime: endTime2 - startTime2,
      following,
      followingTime: endTime3 - startTime3,
    },
  };
};

export default Home;

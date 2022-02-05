import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import NavBar from "../../components/Navbar/Navbar";
import { syncFetchRequest, fetchRequest } from "../../../helpers/fetchRequest";
import "./SingleTonPost.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import {
  faHeart,
  faComment,
  faBookmark,
} from "@fortawesome/free-regular-svg-icons";
import {
  faHeart as faHeartFilled,
  faBookmark as faBookmarkFilled,
} from "@fortawesome/free-solid-svg-icons";
import Loader from "react-loader-spinner";
import { nFormatter } from "../../../helpers/numbers";

import ReactReadMoreReadLess from "react-read-more-read-less";

function SingleTonPost() {
  const { postId } = useParams();
  const [loading, setLoading] = useState(false);
  const [postImage, setPostImage] = useState("");
  const [comments, setComments] = useState([]);
  const [comment, setComment] = useState("");
  const [timeDiff, setTimeDiff] = useState("");
  const [likes, setLikes] = useState(0);
  const [userData, setUserData] = useState({});
  const [requestUserHasLiked, setRequestUserHasLiked] = useState(false);
  const [requestUserHasBookmarked, setRequestUserHasBookmarked] =
    useState(false);
  const [postUserData, setPostUserData] = useState({})
  const toggleLike = () => {
    if (requestUserHasLiked) {
      removeLike();
    } else {
      addLike();
    }
  };
  const toggleBookmark = () => {
    if (requestUserHasBookmarked) {
      removeBookmark();
    } else {
      addBookmark();
    }
  };
  const addLike = async () => {
    if (!requestUserHasLiked) {
      fetchRequest({
        path_: "/api/addLike/",
        method: "POST",
        body: { custom_id: props.postData.custom_id },
        next: (data) => {
          if (data.response === "Liked") {
            setRequestUserHasLiked(true);
            setLikes(likes + 1);
          }
        },
      });
    }
  };
  const removeLike = async () => {
    if (requestUserHasLiked) {
      fetchRequest({
        path_: "/api/removeLike/",
        method: "POST",
        body: { custom_id: props.postData.custom_id },
        next: (data) => {
          if (data.response === "Like Removed") {
            setRequestUserHasLiked(false);
            setLikes(likes - 1);
          }
        },
      });
    }
  };
  const addBookmark = async () => {
    if (!requestUserHasBookmarked) {
      fetchRequest({
        path_: "/api/addBookmark/",
        method: "POST",
        body: { custom_id: props.postData.custom_id },
        next: (data) => {
          if (data.response === "Bookmarked") {
            setRequestUserHasBookmarked(true);
          }
        },
      });
    }
  };
  const removeBookmark = async () => {
    if (requestUserHasBookmarked) {
      fetchRequest({
        path_: "/api/removeBookmark/",
        method: "POST",
        body: { custom_id: props.postData.custom_id },
        next: (data) => {
          if (data.response === "Bookmark Removed") {
            setRequestUserHasBookmarked(false);
          }
        },
      });
    }
  };

  const handleCommentChange = (e) => {
    setComment(e.target.value);
  };


  const commentFunction = () => {
    console.log(comment)
  };

  const getPostData = () => {
    setLoading(true);
    syncFetchRequest({
      path_: "/api/getPostData/",
      method: "POST",
      body: { custom_id: postId },
      next: (data) => {
        console.log(data.response);
        setLikes(data.response.likes);
        setPostImage(data.response.post_image);
        setTimeDiff(data.response.time_diff);
        setRequestUserHasLiked(data.response.wasLiked);
        setRequestUserHasBookmarked(data.response.wasBookmarked);
        setLoading(false);
        setPostUserData(data.response.user_data)
      },
    });
  };

  useEffect(() => {
    getPostData();
  }, []);

  return (
    <>
      <NavBar setUserData={setUserData} />
      <div
        className="loader container-fluid"
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        {loading ? (
          <Loader
            type="TailSpin"
            color="blue"
            height={50}
            width={50}
            timeout={30000}
            id="loader"
          />
        ) : (
          ""
        )}
      </div>

      {postImage && <div className="white-box-post-single">
        <div className="sp__left">
          <div className="image">
            <img src={postImage} className="postImage" />
          </div>
        </div>
        <div className="sp__right">
          <div className="header container-fluid d-flex p-2 align-items-center ">
            <a href={"/" + postUserData.username + "/"}>
            <img className="post-dp-img" src={postUserData.dp_url} alt="" />
            </a>

            <a href={"/" + postUserData.username + "/"} className="link" style={{ marginLeft: "7px" }}>
              <b>{postUserData.username}</b>
            </a>
          </div>
          <div className="comments">
            
          </div>
          <div className="icons-container">
            <div className="icons py-2">
            <div className="left mx-2">
            {requestUserHasLiked ? (
              <FontAwesomeIcon
                onClick={toggleLike}
                icon={faHeartFilled}
                color="red"
                size={"2x"}
                style={{ marginRight: "10px" }}
              />
            ) : (
              <FontAwesomeIcon
                onClick={toggleLike}
                icon={faHeart}
                color="black"
                size={"2x"}
                style={{ marginRight: "10px" }}
              />
            )}
            <FontAwesomeIcon
              icon={faComment}
              size={"2x"}
              onClick={() => {
                window.location.pathname =
                  "/post/" + props.postData.custom_id + "/";
              }}
            />
          </div>
          <div className="right mx-2">
            {requestUserHasBookmarked ? (
              <FontAwesomeIcon
                icon={faBookmarkFilled}
                color="black"
                size={"2x"}
                onClick={toggleBookmark}
              />
            ) : (
              <FontAwesomeIcon
                onClick={toggleBookmark}
                icon={faBookmark}
                color="black"
                size={"2x"}
              />
            )}
          </div>
            </div>
          <div className="other-info px-3" style={{ display: "flex"}}>
          <div className="left">{nFormatter(likes)} likes</div>
          <div className="right" >
            {timeDiff}
          </div>
          </div>
          </div>
          <div className="post-comment">
            <div className="input-box">
            <img src={userData.dp_url} alt="" className="post-dp-img" />
            <input id="cmnt" style={{textAlign: "left"}} type="text" onChange={handleCommentChange} placeholder="Comment Something"/>
            <FontAwesomeIcon icon={faPaperPlane}
                color="blue"
                size={"2x"}
                onClick={commentFunction}/>
            </div>
          </div>
        </div>
      </div>}
    </>
  );
}

export default SingleTonPost;

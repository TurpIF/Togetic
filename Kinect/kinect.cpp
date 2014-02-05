#include <iostream>

#define __STDC_FORMAT_MACROS
#include <inttypes.h>

#include "kinect.h"

#include <NiteSampleUtilities.h>

#define MIN_NUM_CHUNKS(data_size, chunk_size)	((((data_size)-1) / (chunk_size) + 1))
#define MIN_CHUNKS_SIZE(data_size, chunk_size)	(MIN_NUM_CHUNKS(data_size, chunk_size) * (chunk_size))

Kinect* Kinect::ms_self = NULL;

Kinect::Kinect(const char* strSampleName, float * x, float * y, float * z) : m_poseUser(0)
{
  ms_self = this;
  strncpy(m_strSampleName, strSampleName, ONI_MAX_STR);
  m_pUserTracker = new nite::UserTracker;
  m_x = x;
  m_y = y;
  m_z = z;
}

Kinect::~Kinect()
{
  Finalize();
  delete[] m_pTexMap;
  ms_self = NULL;
}

void Kinect::Finalize()
{
  delete m_pUserTracker;
  nite::NiTE::shutdown();
  openni::OpenNI::shutdown();
}

openni::Status Kinect::Init(int argc, char **argv)
{
  m_pTexMap = NULL;

  openni::Status rc = openni::OpenNI::initialize();
  if (rc != openni::STATUS_OK)
  {
    printf("Failed to initialize OpenNI\n%s\n", openni::OpenNI::getExtendedError());
    return rc;
  }

  const char* deviceUri = openni::ANY_DEVICE;
  rc = m_device.open(deviceUri);
  if (rc != openni::STATUS_OK)
  {
    printf("Failed to open device\n%s\n", openni::OpenNI::getExtendedError());
    return rc;
  }

  nite::NiTE::initialize();

  if (m_pUserTracker->create(&m_device) != nite::STATUS_OK)
  {
    return openni::STATUS_ERROR;
  }

  return openni::STATUS_OK;
}
openni::Status Kinect::Run()
{
  std::cout << "running..." << std::endl << std::flush;
  while(true) {
    Update();
  }
  return openni::STATUS_OK;
}

#define MAX_USERS 1
bool g_visibleUsers[MAX_USERS] = {false};
nite::SkeletonState g_skeletonStates[MAX_USERS] = {nite::SKELETON_NONE};
char g_userStatusLabels[MAX_USERS][100] = {{0}};
char g_generalMessage[100] = {0};

#define USER_MESSAGE(msg) {\
  sprintf(g_userStatusLabels[user.getId()], "%s", msg);\
  printf("[%08" PRIu64 "] User #%d:\t%s\n", ts, user.getId(), msg);}

void updateUserState(const nite::UserData& user, uint64_t ts)
{
  if (user.isNew())
  {
    USER_MESSAGE("New");
  }
  else if (user.isVisible() && !g_visibleUsers[user.getId()])
    printf("[%08" PRIu64 "] User #%d:\tVisible\n", ts, user.getId());
  else if (!user.isVisible() && g_visibleUsers[user.getId()])
    printf("[%08" PRIu64 "] User #%d:\tOut of Scene\n", ts, user.getId());
  else if (user.isLost())
  {
    USER_MESSAGE("Lost");
  }
  g_visibleUsers[user.getId()] = user.isVisible();


  if(g_skeletonStates[user.getId()] != user.getSkeleton().getState())
  {
    switch(g_skeletonStates[user.getId()] = user.getSkeleton().getState())
    {
      case nite::SKELETON_NONE:
        USER_MESSAGE("Stopped tracking.")
          break;
      case nite::SKELETON_CALIBRATING:
        USER_MESSAGE("Calibrating...")
          break;
      case nite::SKELETON_TRACKED:
        USER_MESSAGE("Tracking!")
          break;
      case nite::SKELETON_CALIBRATION_ERROR_NOT_IN_POSE:
      case nite::SKELETON_CALIBRATION_ERROR_HANDS:
      case nite::SKELETON_CALIBRATION_ERROR_LEGS:
      case nite::SKELETON_CALIBRATION_ERROR_HEAD:
      case nite::SKELETON_CALIBRATION_ERROR_TORSO:
        USER_MESSAGE("Calibration Failed... :-|")
          break;
    }
  }
}

void Kinect::UpdateXYZ(nite::UserTracker* pUserTracker, const nite::UserData& userData)
{
  nite::SkeletonJoint head = userData.getSkeleton().getJoint(nite::JOINT_HEAD);
  //std::cout << head.getPositionConfidence() << std::endl << std::flush;
  //if (head.getPositionConfidence() >= 0.5) {
  // *m_x = head.getPosition().x;
  // *m_y = head.getPosition().y;
  // *m_z = head.getPosition().z;
  std::cout << "POS " << head.getPosition().x
    << " " << head.getPosition().y
    << " " << head.getPosition().z
    << std::endl << std::flush;
  //}
}


void Kinect::Update()
{
  nite::UserTrackerFrameRef userTrackerFrame;
  openni::VideoFrameRef depthFrame;
  nite::Status rc = m_pUserTracker->readFrame(&userTrackerFrame);
  if (rc != nite::STATUS_OK)
  {
    printf("GetNextData failed\n");
    return;
  }

  const nite::Array<nite::UserData>& users = userTrackerFrame.getUsers();
  for (int i = 0; i < users.getSize(); ++i)
  {
    const nite::UserData& user = users[i];

    updateUserState(user, userTrackerFrame.getTimestamp());
    if (user.isNew())
    {
      m_pUserTracker->startSkeletonTracking(user.getId());
      // m_pUserTracker->startPoseDetection(user.getId(), nite::POSE_CROSSED_HANDS);
    }
    else if (!user.isLost())
    {
      if (users[i].getSkeleton().getState() == nite::SKELETON_TRACKED)
      {
        UpdateXYZ(m_pUserTracker, user);
      }
    }
  }
}

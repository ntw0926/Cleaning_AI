import sys
sys.path.append('d:\\Assignment\\graduate\\Cleaning_AI\\main_code')
import os
from GameTrain_Ai import *

def main():
    print(env)
    model = PPO.load(CHECKPOINT_DIR+"/best_model_10000000")
    
    for episode in range(5):
        obs = env.reset()[0]
        print("episode " + str(episode) + " start")
        total_reward = 0
        done = False
        turncated = False
        step = 0
        while (not done) and (not turncated) : 
            action, state = model.predict(obs)
            obs, reward, done, turncated, info = env.step(int(action))
            total_reward += reward
            time.sleep(0.02)
            step += 1
        pygame.image.save(env.screen, model_text + "_" + map_text + "_" + str(episode) + ".PNG" )
        print('Total Reward for episode {} is {} / step taken {}'.format(episode, total_reward, step))

if __name__ == "__main__":
    main()
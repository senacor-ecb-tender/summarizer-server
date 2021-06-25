<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title class="ecb-font-bold">
          Text Summarizer
        </q-toolbar-title>
        <q-space/>
        <div class="q-gutter-sm row items-center no-wrap ecb-font-regular">
          <q-btn size="sm" push color="white" text-color="primary" label="Summarize" icon="menu_book"
                 v-if="$q.screen.gt.sm" @click="openDialog = true">
            <q-tooltip>Run summarization</q-tooltip>
          </q-btn>
          <q-space/>

        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      bordered
      content-class="bg-white"
    >
      <q-list>
        <q-item-label
          header
          class="text-primary text-bold ecb-font-regular"
        >
          Our Application
        </q-item-label>
        <EssentialLink
          v-for="link in linksDataMain"
          :key="link.title"
          v-bind="link"
        />
        <q-item-label
          header
          class="text-primary text-bold ecb-font-regular"
        >
          Used Frameworks
        </q-item-label>
        <EssentialLink
          v-for="link in linksDataFrameworks"
          :key="link.title"
          v-bind="link"
        />
        <q-item-label
          header
          class="text-primary text-bold ecb-font-regular"
        >
          Infrastructure
        </q-item-label>
        <EssentialLink
          v-for="link in linksDataInfrastructure"
          :key="link.title"
          v-bind="link"
        />
      </q-list>

    </q-drawer>

    <q-dialog v-model="openDialog" @close="reset" @hide="reset" full-width full-height>
      <div class="row" style="overflow: auto; height: inherit;">
        <div class="col-3" style="background-color: white;">
          <q-card style="overflow: auto;" flat square>
            <q-card-section>
              <div class="text-h6 text-primary">Setup</div>
            </q-card-section>
            <q-card-section>
              <q-select
                style="overflow: auto;"
                outlined
                dense
                v-model="topicType"
                :options="optionsTopic"
                option-label="label"
                option-value="id"
                label="Select Topic">
                <template v-slot:prepend>
                  <q-icon name="my_location"/>
                </template>
              </q-select>
            </q-card-section>
            <q-card-section>
              <q-select
                style="overflow: auto;"
                outlined
                dense
                v-model="summaryType"
                :options="optionsSummary"
                option-label="label"
                option-value="id"
                label="Select Size Of Summary">
                <template v-slot:prepend>
                  <q-icon name="article"/>
                </template>
              </q-select>
            </q-card-section>
            <q-card-section>
              <q-uploader
                style="overflow: auto; width: inherit"
                label="Textfile"
                :factory="factoryFn"
                @uploaded="summarize"
                @failed="failed"
                @added="setFileSelected"
                @removed="unsetFileSelected"
                hide-upload-btn
                color="white"
                text-color="black"
                flat
                bordered
                accept=".txt"
                ref="uploader"
              />
            </q-card-section>
            <q-card-actions align="center">
              <q-btn size="sm" unelevated :disabled="!isComplete" color="primary" label="Summarize"
                     @click="$refs.uploader.upload()">
                <q-tooltip>Run summarization</q-tooltip>
              </q-btn>
              <q-btn size="sm" unelevated color="primary" label="Reset" @click="reset()">
                <q-tooltip>Reset</q-tooltip>
              </q-btn>
              <q-btn size="sm" unelevated color="primary" label="Close" @click="close()">
                <q-tooltip>Close</q-tooltip>
              </q-btn>
            </q-card-actions>
          </q-card>
        </div>
        <q-separator vertical color="primary" size="0.15rem"/>

        <div v-if="summaryVisible" class="col-6" style="background-color: white">
          <q-card flat style="overflow: auto;" square>
            <q-card-section>
              <div class="text-h6 text-primary">Summary</div>
            </q-card-section>

            <q-card-actions>
              <q-btn flat round color="primary" icon="save" @click="exportSummary"/>
            </q-card-actions>
            <q-card-section>
              {{ summarization }}
            </q-card-section>
          </q-card>
        </div>

        <div v-if="summaryVisible" class="col-2" style="background-color: white">
          <q-card flat style="overflow: auto;" square>
            <q-card-section>
              <div class="text-h6 text-primary">Rating</div>
            </q-card-section>

            <q-card-section>
              <q-rating
                v-model="ratingModel"
                size="1.5em"
                color="primary"
                icon="star_border"
                icon-selected="star"
              />
            </q-card-section>
            <q-card-section>
              By rating the quality of the summary you can improve
              the model quality by providing better training data
              for future model tuning.
              <br><br>
              This feature is not implemented yet.
            </q-card-section>
          </q-card>
        </div>
      </div>
    </q-dialog>

    <q-page-container>
      <router-view/>
    </q-page-container>
  </q-layout>


</template>

<script>

import EssentialLink from 'components/EssentialLink.vue'
import {ref} from 'vue'
import {exportFile, useQuasar} from 'quasar'

const linksDataMain = [
  {
    title: 'Docs',
    caption: 'See documentation',
    icon: 'school',
    link: 'https://quasar.dev'
  },
  {
    title: 'Our Code',
    caption: 'See code repository',
    icon: 'code',
    link: 'https://github.com/senacor-ecb-tender/summarizer-server'
  }
];

const linksDataFrameworks = [
  {
    title: 'FastAPI',
    caption: 'ASGI python server',
    icon: 'local_library',
    link: 'https://fastapi.tiangolo.com/'
  },
  {
    title: 'Huggingface',
    caption: 'The AI community',
    icon: 'local_library',
    link: 'https://huggingface.co/'
  },
  {
    title: 'Quasar Framework',
    caption: 'Front-End Framework',
    icon: 'local_library',
    link: 'https://quasar.dev/'
  }
];

const linksDataInfrastructure = [
  {
    title: 'Azure Machine Learning',
    caption: 'Integrated Data Science-Solution',
    icon: 'Isettings_input_composite',
    link: 'https://docs.microsoft.com/de-de/azure/machine-learning/overview-what-is-azure-ml'
  },
  {
    title: 'Azure Kubernetes Service',
    caption: 'Easily manage Kubernetes with Azure',
    icon: 'settings_input_composite',
    link: 'https://azure.microsoft.com/en-us/services/kubernetes-service//'
  },
  {
    title: 'Azure Static Web Apps',
    caption: 'A serverless web app hosting service',
    icon: 'settings_input_composite',
    link: 'https://azure.microsoft.com/en-us/services/app-service/static'
  },
  {
    title: 'GitHub',
    caption: 'Manage your code',
    icon: 'settings_input_composite',
    link: 'https://github.com/'
  }
];

export default {
  name: 'MainLayout',
  components: {EssentialLink},
  data() {
    return {
      leftDrawerOpen: false,
      linksDataMain: linksDataMain,
      linksDataFrameworks: linksDataFrameworks,
      linksDataInfrastructure: linksDataInfrastructure,


      optionsTopic: [
        {
          id: 'asset_quality',
          label: 'Asset Quality'
        },
        {
          id: 'climate_risk',
          label: 'Climate Risk'
        },
        {
          id: 'pandemic',
          label: 'Pandemic'
        },
        {
          id: 'credit_lending',
          label: 'Credit Lending'
        }
      ],
      optionsSummary: [
        {
          id: 'long',
          label: 'Long version (9-15 sentences)'
        },
        {
          id: 'short',
          label: 'Short version (3-6 sentences)'
        }
      ],
      topicType: "",
      summaryType: "",
      fileSelected: "",
      summarization: "...",
      openDialog: false,
      summaryVisible: false
    }
  },
  setup() {
    const $q = useQuasar()
    return {
      ratingModel: ref(0),
      failed(info) {
        $q.notify({
          type: 'negative',
          message: 'Call to Summarization API failed!'
        })
      }
    }
  },
  computed: {
    isComplete() {
      return this.topicType != "" && this.summaryType != "" && this.fileSelected != "";
    }
  },
  methods: {
    exportSummary() {
      const $q = useQuasar()

      const status = exportFile('summary.txt', this.summarization, {
        encoding: 'UTF-8',
        mimeType: 'text/plain;charset=UTF-8;'
      })

      if (status === true) {
        // browser allowed it
      } else {
        // browser denied it
        $q.notify({
          type: 'negative',
          message: 'Browser does not allow the export: Error code ' + status
        })
      }
    },
    setFileSelected() {
      this.fileSelected = "true"
    },
    unsetFileSelected() {
      this.fileSelected = ""
    },
    reset() {
      this.summaryVisible = false
      this.summaryType = ""
      this.topicType = ""
      this.fileSelected = ""
      this.$refs.uploader.reset()
    },
    close() {
      this.openDialog = false
    },
    factoryFn(files) {
      return {
        url: process.env.API + '/upload',
        method: 'POST',
        fieldName: 'file',
        formFields: [{name: 'topic', value: this.topicType.id}, {name: 'summary_type', value: this.summaryType.id}]
      }
    },
    summarize({files, xhr}) {
      this.summarization = JSON.parse(xhr.response).result
      this.summaryVisible = true
    }
  }
}
</script>
